<!--
This file is part of PyPop

  Copyright (C) 2003. The Regents of the University of California (Regents) 
  All Rights Reserved.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
USA.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,
ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF
REGENTS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF
ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". REGENTS HAS NO OBLIGATION
TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
MODIFICATIONS.
-->
<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <!-- ################  START FILTER OUTPUT  ############# --> 

 <xsl:template match="translateTable">

  <xsl:call-template name="newline"/>
  <xsl:text>Translations (based on alleles in Anthony Nolan database) performed:</xsl:text>

  <xsl:variable name="all-transl" select="translate"/>
  <xsl:variable name="unique-transl" select="translate[not(@input=preceding-sibling::translate/@input)]/@input"/>
  
  <xsl:call-template name="newline"/>
  <xsl:for-each select="$unique-transl">
   <xsl:value-of select="."/>
   <xsl:text>-&gt;</xsl:text>
   <xsl:value-of select="$all-transl[@input=current()]/@output"/>
   <xsl:text> (</xsl:text>
   <xsl:value-of select="count($all-transl[@input=current()])"/>
   <xsl:text>)</xsl:text>
   <xsl:if test="position()!=last()">
    <xsl:text>, </xsl:text>
   </xsl:if>
  </xsl:for-each>
   
  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- ################  END FILTER OUTPUT  ############### --> 

</xsl:stylesheet>
<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
 