<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:strip-space elements="*"/>
    <xsl:output indent="yes"/>

    <!-- XSL PARAM -->
    <xsl:param name="item_num"/>

    <xsl:template match="/iati-activity">
        <xsl:apply-templates select="iati-identifier[position()=$item_num]"/>
    </xsl:template>

    <xsl:template match="iati-identifier">
        <iati-activity>
            <xsl:copy-of select="."/>
            <xsl:copy-of select="following-sibling::reporting-org[1]"/>
            <xsl:copy-of select="following-sibling::narrative[1]"/>
            <xsl:copy-of select="following-sibling::title[1]"/>
            <xsl:copy-of select="following-sibling::description[1]"/>
            <xsl:copy-of select="following-sibling::participating-org[1]"/>
            <xsl:copy-of select="following-sibling::activity-status[1]"/>
            <xsl:copy-of select="following-sibling::activity-date[1]"/>
            <xsl:copy-of select="following-sibling::contact-info[1]"/>
            <xsl:copy-of select="following-sibling::organisation[1]"/>
            <xsl:copy-of select="following-sibling::telephone[1]"/>
            <xsl:copy-of select="following-sibling::email[1]"/>
            <xsl:copy-of select="following-sibling::mailing-address[1]"/>
            <xsl:copy-of select="following-sibling::recipient-country[1]"/>
            <xsl:copy-of select="following-sibling::sector[1]"/>
            <xsl:copy-of select="following-sibling::collaboration-type[1]"/>
            <xsl:copy-of select="following-sibling::default-flow-type[1]"/>
            <xsl:copy-of select="following-sibling::default-finance-type[1]"/>
            <xsl:copy-of select="following-sibling::default-tied-status[1]"/>
            <xsl:copy-of select="following-sibling::transaction[1]"/>
            <xsl:copy-of select="following-sibling::transaction-type[1]"/>
            <xsl:copy-of select="following-sibling::transaction-date[1]"/>
            <xsl:copy-of select="following-sibling::value[1]"/>
            <xsl:copy-of select="following-sibling::conditions[1]"/>
        </iati-activity>
    </xsl:template>

</xsl:stylesheet>